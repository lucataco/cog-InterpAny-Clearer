# / Cog model

This is an implementation of [](https://github.com/) as a [Cog](https://github.com/replicate/cog) model.

## Development

Follow the [model pushing guide](https://replicate.com/docs/guides/push-a-model) to push your own model to [Replicate](https://replicate.com).

## Basic Usage

Download weights first

    cog run script/download_weights

Then for predictions,

    cog predict -i video=@demo/demo.mp4


# Example

![alt text](output.gif)
