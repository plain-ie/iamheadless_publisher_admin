var IAMHEADLESS_READABILITY_FORM_FIELD_SCORE_CLASS_NAME = 'iamheadless_readability_field_readability_score';


function ReadableFormField(field){
    this.field = field;
    this.add_score_listener = function(element){
        var self = this;
        self.field.addEventListener('keyUp', function(e){
            var value = e.target_element.value;
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
            if (xhttp.readyState == 4 && xhttp.status == 200)
                var response_data = JSON.parse(xhttp.responseText)
                var reading_score = response_data.reading_score;
                var reading_ease = response_data.reading_ease;
                element.innerHTML = reading_score;
                element.className = IAMHEADLESS_READABILITY_FORM_FIELD_SCORE_CLASS_NAME + ' ' + reading_ease;
            }
            xhttp.open("GET", theUrl, true);
            xhttp.send({'text': value});
        });
    };
    this.add_score_output_element = function(){
        var self = this;
        var element = document.createElement('span');
        element.className = IAMHEADLESS_READABILITY_FORM_FIELD_SCORE_CLASS_NAME;
        self.field.parentNode.insertBefore(element, self.field.nextSibling)
        return element;
    };
    this.init = function(){
        var self = this;
        var selector = '.' + IAMHEADLESS_READABILITY_FORM_FIELD_SCORE_CLASS_NAME;
        var score_output_siblings = self.field.parentNode.querySelectorAll(selector);
        if (score_output_siblings.length === 0){
            var score_output_element = self.add_score_output_element();
            self.add_score_listener(score_output_element);
        };
    };
    this.init();
};


function DetectReadableFormFields(){
    this.init = function(selector){
        var elements = document.querySelectorAll(selector);
        for (var i = 0; i < elements.length; i++){
            new ReadableFormField(elements[i]);
        };
    };
    this.init();
};
