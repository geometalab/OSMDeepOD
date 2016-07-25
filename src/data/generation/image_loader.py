from src.data.multi_loader import MultiLoader
from src.data.url_builder import UrlBuilder
from src.data.generation.crosswalk_image import CrosswalkImage


class ImageLoader:
    def __init__(self):
        pass

    def get_images(self, nodes):
        url_builder = UrlBuilder()
        crosswalk_images = []
        for node in nodes:
            url = url_builder.get_url_by_node(node)
            crosswalk_images.append(CrosswalkImage(node=node, url=url))
        urls = [crosswalk_image.url for crosswalk_image in crosswalk_images]
        images = self._download_images(urls)
        self._set_tile_image(images, crosswalk_images)
        return self._get_cropped_images(crosswalk_images)

    @staticmethod
    def _download_images(urls):
        loader = MultiLoader.from_url_list(urls)
        loader.download()
        return loader.results

    @staticmethod
    def _set_tile_image(images, crosswalk_images):
        for crosswalk_image in crosswalk_images:
            for image in images:
                if image.filename == crosswalk_image.url:
                    crosswalk_image.tile_image = image

    @staticmethod
    def _get_cropped_images(crosswalk_images):
        cropped_images = []
        for crosswalk_image in crosswalk_images:
            image = crosswalk_image.crop_tile_image()
            if image is not None:
                cropped_images.append(image)
        return cropped_images
