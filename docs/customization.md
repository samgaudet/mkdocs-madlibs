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

## Controlling user inputs

MkDocs Mad Libs uses the `contenteditable` HTML attribute to make code snippets editable.
By default, this enables users to create any valid content within the `<span>` tag.

To control what keyboard inputs are valid for a user to make use of,
you can add a JavaScript `EventListener`.

### Add custom Javascript dependency

Follow the general `mkdocs-material` instructions for
[adding custom JavaScript](https://squidfunk.github.io/mkdocs-material/customization/#additional-javascript).

```yaml title="mkdocs.yml"
extra_javascript:
    - javascripts/extra.js
```

### Select all the Mad Libs HTML content

Using the `madlibs-editable` class that is added to all Mad Libs editable content,
you can select all the elements that need to be modified.

```js title="extra.js"
let madlibsEditableContent = document.querySelectorAll(".madlibs-editable");
```

### Add an event listener

Using the editable content elements queried from the HTML document,
add an event listener for the [keydown event](https://developer.mozilla.org/en-US/docs/Web/API/Element/keydown_event).

```js title="extra.js"
let madlibsEditableContent = document.querySelectorAll(".madlibs-editable");

for (i = 0; i < madlibsEditableContent.length; i++) {
    madlibsEditableContent[i].addEventListener("keydown", event => {
        console.log(event)
    });
};
```

### Add logic to restrict the user inputs

Use the [`KeyboardEvent`](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent)
objects to apply constraints of your choosing, for example:

```js title="extra.js"
let madlibsEditableContent = document.querySelectorAll(".madlibs-editable");

for (i = 0; i < madlibsEditableContent.length; i++) {
    madlibsEditableContent[i].addEventListener("keydown", event => {
        // prevent the user from backspacing if the content is empty
        if (event.key == "Backspace" && event.target.textContent === "") {
            event.preventDefault()
        };
        // prevent the user from adding newlines
        if (event.key == "Enter") {
            event.preventDefault()
        };
    });
};
```
