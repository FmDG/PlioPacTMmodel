

def within_stddev(dataset, parameter, num_devs=2):
    """
    Returns the dataset with all values that are outside of the standard deviation * 'num-devs' of the mean.
    :param dataset:
    :param parameter:
    :param num_devs:
    :return: the dataset selecting only those values which aren't extreme
    """
    return dataset[
        dataset[parameter].between(
            dataset[parameter].mean() - (num_devs * dataset[parameter].std()),
            dataset[parameter].mean() + (num_devs * dataset[parameter].std()))
    ]
