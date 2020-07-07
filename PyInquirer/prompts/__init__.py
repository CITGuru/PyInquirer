class PromptParameterException(ValueError):
    def __init__(self, message, errors=None):

        # Call the base class constructor with the parameters it needs
        super(PromptParameterException, self).__init__(
            'You must provide a `%s` value' % message, errors)
