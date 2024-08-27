import { LitElement, html, css } from "lit";
import { Streamlit } from "streamlit-component-lib";

class MyButton extends LitElement {
  static BUTTON_HEIGHT = 50;

  static styles = css`
    :host {
      display: block;
      width: 150px;
      height: ${MyButton.BUTTON_HEIGHT}px;
    }
    button {
      background-color: blue;
      color: white;
      padding: 0px 0px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 16px;
      width: 100%;
      height: 100%;
    }
  `;

  render() {
    return html` <button @click=${this.handleClick}>Click Me</button> `;
  }

  firstUpdated() {
    // Adjust the iframe height to 100%
    const iframe = window.frameElement;
    if (iframe) {
      iframe.style.height = `${MyButton.BUTTON_HEIGHT}px`;
      iframe.style.width = "100%";
      iframe.setAttribute("height", `${MyButton.BUTTON_HEIGHT}px`);
      iframe.setAttribute("width", "100%");
    }

    // Notify Streamlit that the component is ready
    Streamlit.setComponentReady();

    // Set the height dynamically to ensure the iframe adjusts to content
    Streamlit.setFrameHeight(window.document.body.scrollHeight);
  }

  handleClick() {
    console.log("Button clicked!");
    // Notify Streamlit about the click event
    Streamlit.setComponentValue("Button clicked!");
  }

  // firstUpdated() {
  //   // Ensure this code runs after rendering
  //   const button = document.querySelector("my-button");
  //   console.log(button);
  //   console.log(button.clientHeight);
  //   console.log(button.offsetHeight);
  //   console.log(button.scrollHeight);
  //   if (button) {
  //     const buttonHeight = this.BUTTON_HEIGHT + 16;
  //     // debugger;
  //     // const buttonHeight = 50;

  //     // Adjust the iframe height to match the button's height
  //     const iframe = window.frameElement;
  //     if (iframe) {
  //       iframe.style.height = `${buttonHeight}px`;
  //       iframe.style.width = "100%";
  //       iframe.setAttribute("height", `${buttonHeight}`);
  //       iframe.setAttribute("width", "100%");
  //     }
  //   }

  //   // Notify Streamlit that the component is ready
  //   Streamlit.setComponentReady();
  //   // Set the frame height dynamically based on content
  //   Streamlit.setFrameHeight(buttonHeight);
  // }
}

customElements.define("my-button", MyButton);

// Ensure Streamlit is ready before using it
// Streamlit.setComponentReady();
// Streamlit.setFrameHeight(60);
