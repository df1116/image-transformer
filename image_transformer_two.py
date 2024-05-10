import random


class ImageSamplerTwo:
    def __init__(self, img):
        self.image = img
        self.image_width, self.image_height = img.size
        self.sample_width = None
        self.sample_height = None

    def get_samples(self, sample_width, sample_height):
        """Randomly selects a specified number of distinct samples from the image."""
        self.validate_sample_size(sample_width, sample_height)
        self.sample_width = sample_width
        self.sample_height = sample_height

        # FIRST SAMPLE
        possible_coordinates = set()

        # Horizontal and Vertical starting positions
        possible_coordinates = self.add_coordinates(possible_coordinates, self.coordinates(samples_left=2))
        possible_coordinates = self.add_coordinates(possible_coordinates,
                                                    self.coordinates(samples_left=1, samples_right=1))
        possible_coordinates = self.add_coordinates(possible_coordinates, self.coordinates(samples_right=2))
        possible_coordinates = self.add_coordinates(possible_coordinates, self.coordinates(samples_above=2))
        possible_coordinates = self.add_coordinates(possible_coordinates,
                                                    self.coordinates(samples_above=1, samples_below=1))
        possible_coordinates = self.add_coordinates(possible_coordinates, self.coordinates(samples_below=2))
        # Diagonal and adjacent starting positions
        possible_coordinates = self.add_coordinates(possible_coordinates,
                                                    self.coordinates(samples_left=1, samples_above=1))
        possible_coordinates = self.add_coordinates(possible_coordinates,
                                                    self.coordinates(samples_right=1, samples_above=1))
        possible_coordinates = self.add_coordinates(possible_coordinates,
                                                    self.coordinates(samples_left=1, samples_below=1))
        possible_coordinates = self.add_coordinates(possible_coordinates,
                                                    self.coordinates(samples_right=1, samples_below=1))
        if not possible_coordinates:
            raise ValueError("Not enough space to fit the 3 samples.")

        # Top left corner of first sample
        starting_point_one = random.choice(tuple(possible_coordinates))

        # SECOND SAMPLE
        possible_coordinates = set()
        to_exclude = set()
        to_exclude = self.add_coordinates(to_exclude, self.get_exclusion_zone(starting_point_one))
        # Horizontal and Vertical starting positions
        possible_coordinates = self.add_coordinates(possible_coordinates, self.coordinates(samples_left=1), to_exclude)
        possible_coordinates = self.add_coordinates(possible_coordinates, self.coordinates(samples_right=1), to_exclude)
        possible_coordinates = self.add_coordinates(possible_coordinates, self.coordinates(samples_above=1), to_exclude)
        possible_coordinates = self.add_coordinates(possible_coordinates, self.coordinates(samples_below=1), to_exclude)
        if not possible_coordinates:
            raise ValueError("Not enough space to fit the 3 samples.")

        # Top left corner of second sample
        starting_point_two = random.choice(tuple(possible_coordinates))

        # THIRD SAMPLE
        possible_coordinates = set()
        to_exclude = self.add_coordinates(to_exclude, self.get_exclusion_zone(starting_point_two))
        possible_coordinates = self.add_coordinates(possible_coordinates, self.coordinates(0, 0, 0, 0), to_exclude)
        if not possible_coordinates:
            raise ValueError("Not enough space to fit the 3 samples.")

        # Top left corner of third sample
        starting_point_three = random.choice(tuple(possible_coordinates))

        samples = [
            self.crop_sample(starting_point_one),
            self.crop_sample(starting_point_two),
            self.crop_sample(starting_point_three)
        ]
        return samples

    def validate_sample_size(self, sample_width, sample_height):
        """Check if the sample size is valid for the given image."""
        img_width, img_height = self.image.size
        if sample_width <= 0 or sample_height <= 0:
            raise ValueError("Sample width and height must be greater than zero.")
        elif sample_width > img_width or sample_height > img_height:
            raise ValueError("Sample size is larger than image dimensions.")

    def coordinates(self, samples_left=0, samples_right=0, samples_above=0, samples_below=0):
        """For a given number of samples that need to be fitted around a new sample get the 2D range of its starting
        point."""
        x_coordinates = [
            samples_left * self.sample_width,
            self.image_width - (samples_right + 1) * self.sample_width
        ]
        y_coordinates = [
            samples_above * self.sample_height,
            self.image_height - (samples_below + 1) * self.sample_height
        ]
        if x_coordinates[0] > x_coordinates[1] or y_coordinates[0] > y_coordinates[1]:
            return []
        return [x_coordinates, y_coordinates]

    @staticmethod
    def add_coordinates(all_coordinates, coordinates, to_exclude=None):
        """Get all the (x, y) coordinates in a 2D range."""
        if not coordinates:
            return all_coordinates
        x_coordinates, y_coordinates = coordinates
        for x in range(x_coordinates[0], x_coordinates[1] + 1):
            for y in range(y_coordinates[0], y_coordinates[1] + 1):
                if to_exclude is None:
                    all_coordinates.add((x, y))
                elif (x, y) not in to_exclude:
                    all_coordinates.add((x, y))
        return all_coordinates

    def get_exclusion_zone(self, point):
        """Given a starting point of a sample get the 2D range it excludes."""
        x, y = point
        return [
            [x - self.sample_width + 1, x + self.sample_width - 1],
            [y - self.sample_height + 1, y + self.sample_height - 1]
        ]

    def crop_sample(self, point):
        """Crop a sample from the parent image."""
        x, y = point
        return self.image.crop((x, y, x + self.sample_width, y + self.sample_height))
