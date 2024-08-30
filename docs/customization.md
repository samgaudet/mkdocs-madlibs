# Customization

!!! tip
    At the moment, only certain aspects of MkDocs Mad Libs are easily configurable.
    If there are other components you feel should be customizable,
    please [_enter a feature request_](https://github.com/samgaudet/mkdocs-madlibs/issues/new?assignees=&labels=enhancement&projects=&template=feature-request-form.yml&title=%5BFeature%20request%5D%3A+).

## Overriding the default styling

MkDocs Mad Libs relies on CSS styling to style the `contenteditable` element used for user input.
This CSS styling is added to your MkDocs site via an extra stylesheet
(see: [_Add custom CSS dependency_](./usage.md#add-custom-css-dependency)).

To override the default styling, modify the `.madlibs-editable` and/or `.madlibs-editable-icon` CSS classes,
where `.madlibs-editable` applies to the editable text,
and `.madlibs-editable-icon` applies to the pen SVG icon adjacent to the text.

Use the default styling as a reference for defining your own styling:
[**extra.css**](https://github.com/samgaudet/mkdocs-madlibs/blob/main/docs/stylesheets/extra.css).
