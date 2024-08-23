document.addEventListener("DOMContentLoaded", () => {
    const editableElements = document.querySelectorAll(".madlibs-editable");
    const primaryColor = getComputedStyle(
      document.documentElement,
    ).getPropertyValue("--md-primary-fg-color");
  
    editableElements.forEach((element) => {
      const svgString = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path d="M290.7 93.2l128 128-278 278-114.1 12.6C11.4 513.5-1.6 500.6 .1 485.3l12.7-114.2 277.9-277.9zm207.2-19.1l-60.1-60.1c-18.8-18.8-49.2-18.8-67.9 0l-56.6 56.6 128 128 56.6-56.6c18.8-18.8 18.8-49.2 0-67.9z" fill="${primaryColor}"/></svg>`;
      const encodedSvg = encodeURIComponent(svgString);
      element.style.backgroundImage = `url("data:image/svg+xml; utf8,${encodedSvg}")`;
    });
  });
  