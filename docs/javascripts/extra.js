// get all the madlibs contenteditable spans
let madlibsEditableContent = document.querySelectorAll(".madlibs-editable");

// allowlist of commands that should be accessible in contenteditable spans
// inspired by the following list:
// https://github.com/tinymce/tinymce/issues/6667#issuecomment-814603922
const metaKeyAllowList = [
    "ArrowUp", // move to top
    "ArrowDown", // move to bottom
    "ArrowLeft", // move to start of line
    "ArrowRight", // move to end of line
    "a", // select all
    "c", // copy
    "v", // paste
    "z", // undo
];

for (i = 0; i < madlibsEditableContent.length; i++) {
    madlibsEditableContent[i].addEventListener("keydown", event => {
        // restrict the set of commands a user can execute in a contenteditable
        if ((event.metaKey || event.ctrlKey) && !metaKeyAllowList.includes(event.key)) {
            event.preventDefault()
        };
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
