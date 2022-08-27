"""
src/rumps_ext.py

written by: Oliver Cordes 2021-03-31
changed by: Oliver Cordes 2022-08-27


"""

from rumps.rumps import Response, _internal, text_type, string_types, _log

from AppKit import NSAlert

class SimpleDialog(object):
    def __init__(self, message='', title='', ok=None, cancel=None, 
                    dimensions=(320, 160) ):
        message = text_type(message)
        message = message.replace('%', '%%')
        title = text_type(title)

        self._cancel = bool(cancel)
        self._icon = None

        _internal.require_string_or_none(ok)
        if not isinstance(cancel, string_types):
            cancel = 'Cancel' if cancel else None

        self._alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
            title, ok, cancel, None, message)
        self._alert.setAlertStyle_(0)  # informational style

        #self._alert.setAccessoryView_(self._textfield)

        #self.default_text = default_text


    @property
    def title(self):
        """
        The text positioned at the top of the window in larger font. If not a
        string, will use the string
        representation of the object.
        """
        return self._alert.messageText()


    @title.setter
    def title(self, new_title):
        new_title = text_type(new_title)
        self._alert.setMessageText_(new_title)


    @property
    def message(self):
        """
        The text positioned below the :attr:`title` in smaller font. If not a
         string, will use the string
        representation of the object.
        """
        return self._alert.informativeText()


    @message.setter
    def message(self, new_message):
        new_message = text_type(new_message)
        self._alert.setInformativeText_(new_message)


    @property
    def icon(self):
        """
        The path to an image displayed for this window. If set to ``None``, 
        will default to the icon for the application using :attr:`rumps.App.icon`.

        .. versionchanged:: 0.2.0
           If the icon is set to an image then changed to ``None``, it will 
           correctly be changed to the application icon.

        """
        return self._icon

    @icon.setter
    def icon(self, icon_path):
        new_icon = _nsimage_from_file(
            icon_path) if icon_path is not None else None
        self._icon = icon_path
        self._alert.setIcon_(new_icon)


    def add_button(self, name):
        """
        Create a new button.

        .. versionchanged:: 0.2.0
           The `name` parameter is required to be a string.

        :param name: the text for a new button. Must be a string.
        """
        _internal.require_string(name)
        self._alert.addButtonWithTitle_(name)


    def add_buttons(self, iterable=None, *args):
        """
        Create multiple new buttons.

        .. versionchanged:: 0.2.0
            Since each element is passed to :meth:`rumps.Window.add_button`, they
            must be strings.
        """
        if iterable is None:
            return
        if isinstance(iterable, string_types):
            self.add_button(iterable)
        else:
            for ele in iterable:
                self.add_button(ele)
        for arg in args:
            self.add_button(arg)

    def run(self):
        """
        Launch the window. :class:`rumps.Window` instances can be reused to 
        retrieve user input as many times as needed.

        :return: a :class:`rumps.rumps.Response` object that contains the text 
        and the button clicked as an integer.
        """
        _log(self)
        clicked = self._alert.runModal() % 999
        if clicked > 2 and self._cancel:
            clicked -= 1
        #return Response(clicked, text)
        return clicked
