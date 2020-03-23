document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }

  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }

  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function (e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          let input_div = this.$form.querySelector('[data-step="' + this.currentStep + '"] div').parentElement;
          this.input_elements = this.$form.querySelector('[data-step="' + this.currentStep + '"] div').parentElement.querySelectorAll('input')
          console.log(input_div)
          console.log(this.input_elements)
          this.check_lst = [];
          this.value_lst = [];
          this.input_elements.forEach( input => {
            if (this.currentStep === 1 || this.currentStep === 3){
              this.check_lst.push(input.checked)

            }if(this.currentStep === 2 || this.currentStep === 4){
              this.value_lst.push(input.value)
            }
          });
          if (this.check_lst.includes(true)){
            e.preventDefault();
            this.currentStep++;
            this.updateForm();
          }else{
            if(this.check_lst.length > 0){
              alert("Proszę uzupełnić wszystkie dane.")
            }
          }
          if (this.value_lst.includes("") !== true && this.value_lst.length > 0){
            e.preventDefault();
            this.currentStep++;
            this.updateForm();

          }else{
            if (this.value_lst.length > 0){
              alert("Proszę uzupełnić wszystkie dane.")
            }
          }

        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });


    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary
    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
    }
  }

  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
  let institution_cat = document.querySelectorAll('.category');
  let checkbox_cat = document.querySelectorAll('[type="checkbox"]');
  checkbox_cat.forEach(el => {
    el.addEventListener('click', el => {
      let value_lst = [];
      checkbox_cat.forEach(el =>{
        if(el.checked === true){
        value_lst.push(el.value)}
        });
      institution_cat.forEach(category => {
        category.parentElement.parentElement.style.display = 'none';
        value_lst.forEach(el => {
          if (category.innerText.includes(el) === true) {
            category.parentElement.parentElement.style.display = 'block'}
          if (category.innerText.includes(el) === false) {
            category.parentElement.parentElement.style.display = 'none'
          }
        })
      })

    })
  });
  if (document.getElementById('form-next')) {
    let next_button = document.getElementById('form-next');
    let address_form = document.getElementById('address-form');
    let address_inputs = address_form.querySelectorAll('input');
    next_button.addEventListener('click', ev => {
      document.querySelector('.form--steps-instructions').style.display = 'none';
      document.getElementById('bags').innerText = document.querySelector('[name="bags"]').value;
      document.getElementById('address').innerText = document.querySelector('[name="address"]').value;
      document.getElementById('city').innerText = document.querySelector('[name="city"]').value;
      document.getElementById('postcode').innerText = document.querySelector('[name="postcode"]').value;
      document.getElementById('phone').innerText = document.querySelector('[name="phone"]').value;
      document.getElementById('date').innerText = document.querySelector('[name="date"]').value;
      document.getElementById('time').innerText = document.querySelector('[name="time"]').value;
      document.getElementById('more_info').innerText = document.querySelector('[name="more_info"]').value;
      document.querySelectorAll('[name="organization"]').forEach(el => {
        if (el.checked === true) {
          document.getElementById('institution').innerText = el.parentElement.querySelector('.title').innerText
        }
      });

      let categories_list = [];
      checkbox_cat.forEach(checkbox => {
        if (checkbox.checked === true) {
          categories_list.push(checkbox.parentElement.querySelector('.description').innerText)
        }
      });
      document.getElementById('categories').innerText = categories_list.join(', ')
      address_inputs.forEach(input => {
        if (input.value === '') {

        }
      });
    });
  }
});