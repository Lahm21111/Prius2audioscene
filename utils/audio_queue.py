# utils/audio_queue_44100.py
from collections import deque
import numpy as np
from typing import List, Tuple, Optional

class AudioQueue441:
    def __init__(self, sample_rate: int = 44100, channels: int = 56):
        self.fs = int(sample_rate)
        self.ch = int(channels)
        self._buf = deque()  # [(start_ts_ns, pcm[N, ch])]
        self._ns_per_sample = int(1e9 // self.fs)
        self._grid_next_start_ns: Optional[int] = None

    def push(self, ts_ns: int, pcm: np.ndarray):
        """pcm shape=(N,ch) 或 (ch,N)/(N,)；内部统一成 (N,ch) float32"""
        x = np.asarray(pcm)
        if x.ndim == 1:
            x = x[:, None]
        elif x.ndim == 2 and x.shape[0] == self.ch and x.shape[1] != self.ch:
            # 形如 (ch, N) → 转置成 (N, ch)
            x = x.T
        if x.ndim != 2 or x.shape[1] != self.ch:
            raise ValueError(f"AudioQueue: expect (N,{self.ch}), got {x.shape}")
        self._buf.append((int(ts_ns), x.astype(np.float32, copy=False)))
        if self._grid_next_start_ns is None:
            self._grid_next_start_ns = int(ts_ns)

    def _concat(self):
        if not self._buf:
            return None, None
        parts = [b for _, b in self._buf]
        start_ns = self._buf[0][0]
        data = np.concatenate(parts, axis=0)  # (N_total, ch)
        return start_ns, data

    def _pop_left(self, consumed: int):
        while consumed > 0 and self._buf:
            t0, blk = self._buf[0]
            n = blk.shape[0]
            if consumed >= n:
                consumed -= n
                self._buf.popleft()
            else:
                new_t = t0 + consumed * self._ns_per_sample
                self._buf[0] = (new_t, blk[consumed:])
                consumed = 0

    def pull_fixed_windows(self, win_samples: int = 4410, hop_samples: Optional[int] = None
                           ) -> List[Tuple[int, np.ndarray]]:
        """固定窗口（默认 4410 样本 ≈ 100ms@44.1k），返回 [(center_ts_ns, seg(win,ch))]"""
        out: List[Tuple[int, np.ndarray]] = []
        hop = hop_samples or win_samples
        start_ns, data = self._concat()
        if data is None:
            return out
        end_ns = start_ns + (data.shape[0] - 1) * self._ns_per_sample

        while self._grid_next_start_ns is not None:
            # 判断这一窗是否完全在缓冲内
            left_ns = self._grid_next_start_ns
            right_ns = left_ns + (win_samples - 1) * self._ns_per_sample
            if right_ns > end_ns:
                break
            offset = int((left_ns - start_ns) // self._ns_per_sample)
            seg = data[offset:offset + win_samples]  # (win, ch)
            center = left_ns + (win_samples // 2) * self._ns_per_sample
            out.append((int(center), seg))

            # 前进 & 释放已消费
            self._grid_next_start_ns += hop * self._ns_per_sample
            self._pop_left(hop)
            start_ns, data = self._concat()
            if data is None:
                break
            end_ns = start_ns + (data.shape[0] - 1) * self._ns_per_sample
        return out
