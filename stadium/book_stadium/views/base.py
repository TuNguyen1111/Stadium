from book_stadium.forms import UserCreationForm


class Base:
    register_form = UserCreationForm

    # ovirride this method if you need
    def get_default_context(self):
        return {
            'register_form': self.register_form,
        }
