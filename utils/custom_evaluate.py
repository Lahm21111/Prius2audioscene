from nuscenes.eval.detection.evaluate import NuScenesEval

class CustomDetectionEval(NuScenesEval):
    def __init__(self, nusc, config, result_path, eval_set, output_dir, verbose):
        super().__init__(nusc, config, result_path, eval_set, output_dir, verbose)

    def main_agnostic(self, plot_examples=0, render_curves=False):
        for sample_token in self.pred_boxes.sample_tokens:
            for box in self.pred_boxes.boxes[sample_token]:
                box.detection_name = "agnostic"

        for sample_token in self.gt_boxes.sample_tokens:
            for box in self.gt_boxes.boxes[sample_token]:
                box.detection_name = "agnostic"
        self.cfg.class_names = ["agnostic"]
        self.cfg.class_range = {"object": 50.0}
        metrics_summary = super().main(plot_examples, render_curves)
        return metrics_summary