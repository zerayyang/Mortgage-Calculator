def get_mortgage_data(mortgage_data):

    # Return the verified mortgage information as a dictionary
    return mortgage_data.model_dump()


def get_calculation_results(results):

    # Return the verified mortgage calculation results as a dictionary
    return results.model_dump()