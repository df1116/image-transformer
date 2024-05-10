# ImageSampler

`ImageSampler` extracts random samples from an image.

`ImageSamplerTwo` performs the same action but in a more random and slow manner. All instructions on how to use 
`ImageSampler` can be used for `ImageSampleTwo`.



## Requirements

- Python 3.6 or later
- Pillow (PIL Fork)

To install Pillow, run:

```bash
pip install Pillow
```

## Usage

### Initialization

First, import and create an instance of `ImageSampler` by providing an image opened using pillow:

```python
from PIL import Image

from image_transformer import ImageSampler

image = Image("path_to_your_image.jpg")
sampler = ImageSampler(image)
```

### Extracting Samples

To extract image samples, specify the width and height of the samples:

```python
samples = sampler.get_samples(sample_width=100, sample_height=100)
```

This will return a list of PIL Image objects corresponding to the random samples extracted from the image.

### Handling Exceptions

The `ImageSampler` includes checks to ensure that the number of samples and their dimensions are valid. If the 
conditions are not met, a `ValueError` will be raised.

### Transformations

Images can be transformed/processsed either before or after they are sampled, see `test_transformations_work` in 
`test_image_transformer.py`.

## Example

Here is a complete example that loads an image, extracts three 100x100 samples, and displays them:

```python
from PIL import Image

from image_transformer import ImageSampler

image = Image("path_to_your_image.jpg")
sampler = ImageSampler(image)
samples = sampler.get_samples(100, 100)

for idx, sample in enumerate(samples):
    sample.show(title=f"Sample {idx+1}")
```