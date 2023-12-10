import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg

from models.image_view_port import ImageViewPort
from models.mixer import OutputPanel

uiclass, baseclass = pg.Qt.loadUiType("views/mainwindow.ui")


class MainWindow(uiclass, baseclass):
    def __init__(self):
        super().__init__()

        # Window and UI configurations
        self.setupUi(self)
        self.setWindowTitle("Fourier Transform Mixer")
        self.show()

        # Initialize states, signals, and slots
        self._initialize_image_viewers()
        self._initialize_output_viewers()
        self._initialize_slots()

    def _initialize_image_viewers(self):
        self.images = [
            ImageViewPort(
                window=self,
                image_original_viewer=self.image_original_1,
                image_component_viewer=self.image_component_1,
                mode_combo_box=self.image_combo_1,
            ),
            ImageViewPort(
                window=self,
                image_original_viewer=self.image_original_2,
                image_component_viewer=self.image_component_2,
                mode_combo_box=self.image_combo_2,
            ),
            ImageViewPort(
                window=self,
                image_original_viewer=self.image_original_3,
                image_component_viewer=self.image_component_3,
                mode_combo_box=self.image_combo_3,
            ),
            ImageViewPort(
                window=self,
                image_original_viewer=self.image_original_4,
                image_component_viewer=self.image_component_4,
                mode_combo_box=self.image_combo_4,
            ),
        ]

    def _initialize_output_viewers(self):
        self.output_ports = [
            OutputPanel(
                window=self,
                output_viewer=self.image_output_1,
                first_image_combo_box=self.image_1_output_1,
                second_image_combo_box=self.image_2_output_1,
                first_image_mode_compo_box=self.image_1_component_output_1,
                second_image_mode_compo_box=self.image_2_component_output_1,
                component1_weight_slider=self.image_1_output_1_slider,
                component2_weight_slider=self.image_2_output_1_slider,
            ),
            OutputPanel(
                window=self,
                output_viewer=self.image_output_2,
                first_image_combo_box=self.image_1_output_2,
                second_image_combo_box=self.image_2_output_2,
                first_image_mode_compo_box=self.image_1_component_output_2,
                second_image_mode_compo_box=self.image_2_component_output_2,
                component1_weight_slider=self.image_1_output_2_slider,
                component2_weight_slider=self.image_2_output_2_slider,
            ),
        ]

    def _initialize_slots(self) -> None:
        self.region_slider.valueChanged.connect(self._region_slider_value_changed)

    def _region_slider_value_changed(self, value) -> None:
        for image_view_port in self.images:
            image_view_port.draw_region_square(scale=(value / 100))

        # todo need to change calling place
        self._display_mixer_output()

    # todo to be continued
    def _display_mixer_output(self):
        if self.image_1_output_1.currentText() == "Image1":
            if self.images[0].image is not None:
                image_1 = self.images[0].image
                print("image1")

        if self.image_2_output_1.currentText() == "Image2":
            if self.images[0].image is not None:
                image_2 = self.images[1].image
                print("image2")

        if (
            self.image_1_component_output_1.currentText() == "Magnitude"
            and self.image_2_component_output_1.currentText() == "Phase"
        ):
            print("mixing")
            OutputPanel.reconstruct_image_using_magnitude_phase(
                self.output_ports[0], image_1, image_2
            )


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()


if __name__ == "__main__":
    main()
