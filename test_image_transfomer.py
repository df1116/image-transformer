import unittest

from PIL import Image

from image_transformer import ImageSampler


class MyTestCase(unittest.TestCase):
    def assert_value_error_raised(self, sample_width, sample_height):
        image = Image.open("thousand.jpg")
        sampler = ImageSampler(image)
        with self.assertRaises(ValueError):
            sampler.get_samples(sample_width, sample_height)

    def test_invalid_width_or_height_raises(self):
        invalid_dimensions = [
            # Samples larger that image
            (1001, 1), (1, 1001),
            # Samples with negative size or 0
            (0, 1), (-1, 1), (1, 0), (1, -1),
            # 3 samples can't fit within image
            (501, 500), (500, 501)
        ]
        for width, height in invalid_dimensions:
            self.assert_value_error_raised(width, height)

    def assert_samples_are_correctly_returned(self, sample_width, sample_height):
        image = Image.open("thousand.jpg")
        sampler = ImageSampler(image)
        samples = sampler.get_samples(sample_width, sample_height)
        assert len(samples) == 3
        for sample in samples:
            assert sample.width == sample_width
            assert sample.height == sample_height

    def test_samples_are_correctly_returned(self):
        valid_dimensions = [
            (1, 1), (500, 500), (1000, 1), (1, 1000)
        ]
        for width, height in valid_dimensions:
            self.assert_samples_are_correctly_returned(width, height)

    def test_transformations_work(self):
        image = Image.open("eiffel.jpg")
        # Rotate the image by 90 degrees
        image = image.rotate(90)
        sampler = ImageSampler(image)
        samples = sampler.get_samples(300, 300)
        for idx, sample in enumerate(samples):
            # Convert to "L" pixel representation
            sample = sample.convert('L')
            sample.show(title=f"Sample {idx+1}")


if __name__ == '__main__':
    unittest.main()
