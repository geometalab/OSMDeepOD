from src.data.generation.image_loader import ImageLoader
from src.data.generation.crosswalk_loader import CrosswalkLoader
from src.data.generation.crosswalk_detector import CrosswalkDetector


class CrosswalkCollector:
    def __init__(self, bbox=None, hdf5_file=None, image_dir='/tmp/crosswalks'):
        self.bbox = bbox
        self.hdf5_file = hdf5_file
        self.image_dir = self._build_dir_path(image_dir)

    def run(self):
        crosswalk_nodes = self._get_crosswalk_nodes()
        cropped_images = self._get_cropped_images(crosswalk_nodes)
        images = self._detect_crosswalks(cropped_images)
        self._store(images)

    def _get_crosswalk_nodes(self):
        crosswalk_loader = CrosswalkLoader()
        return crosswalk_loader.get_crosswalk_nodes(self.bbox)

    @staticmethod
    def _get_cropped_images(crosswalk_nodes):
        image_loader = ImageLoader()
        return image_loader.get_images(crosswalk_nodes)

    def _detect_crosswalks(self, images):
        crosswalk_detector = CrosswalkDetector(self.hdf5_file)
        return crosswalk_detector.detect(images)

    def _store(self, images):
        for image in images:
            image.save(self.image_dir + image.filename)

    @staticmethod
    def _build_dir_path(dir_path):
        if dir_path.endswith('/'):
            return dir_path
        else:
            return dir_path + '/'
