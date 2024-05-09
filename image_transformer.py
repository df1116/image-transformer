import random


class ImageSampler:
    def __init__(self, image):
        """Initialize the ImageSampler with an image."""
        self.image = image

    def get_samples(self, sample_width, sample_height, num_samples=3):
        """Randomly selects a specified number of distinct samples from the image grid."""
        self.validate_sample_size(sample_width, sample_height)

        grid, grid_width, grid_height = self.create_grid(sample_width, sample_height)

        if len(grid) < num_samples:
            raise ValueError("Not enough grid cells to provide 3 distinct samples.")

        chosen_cells = random.sample(grid, num_samples)
        samples = []
        for cell in chosen_cells:
            m, n = cell
            m_scaled = m * grid_width
            n_scaled = n * grid_height
            x = random.randint(m_scaled, m_scaled + grid_width - sample_width)
            y = random.randint(n_scaled, n_scaled + grid_height - sample_height)
            sample = self.image.crop((x, y, x + sample_width, y + sample_height))
            samples.append(sample)
        return samples

    def validate_sample_size(self, sample_width, sample_height):
        """Check if the sample size is valid for the given image."""
        img_width, img_height = self.image.size
        if sample_width <= 0 or sample_height <= 0:
            raise ValueError("Sample width and height must be greater than zero.")
        elif sample_width > img_width or sample_height > img_height:
            raise ValueError("Sample size is larger than image dimensions.")

    def create_grid(self, sample_width, sample_height):
        """Create a grid of sample coordinates based on the image size and sample dimensions."""
        image_width, image_height = self.image.size
        n, grid_width = self.calculate_dimensions(image_width, sample_width)
        m, grid_height = self.calculate_dimensions(image_height, sample_height)
        return [(x, y) for x in range(n) for y in range(m)], grid_width, grid_height

    def calculate_dimensions(self, image_dimension, sample_dimension):
        """Calculate the number of divisions and the size of each division in the grid."""
        divisions = max(image_dimension // sample_dimension, 1)
        division_size = image_dimension // divisions
        return divisions, division_size
