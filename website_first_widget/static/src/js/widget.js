var ButtonWidget = instance.web.Widget.extend({
    template: 'ButtonWidget', //the name of the HTML template that will be used to display the widget
    init: function(parent, label, action){
        // the constructor. Widgets always have the parent widget as
        // first constructor parameter
    this._super(parent);
        this.label = label || 'Button';
        this.action = action || function(){};
    },
    start: function(){
        // start() is called when the DOM has been rendered. This
        // is where we can register callbacks. And we do just that
        // by registering the provided action to the click event on
        // the root DOM element of the widget (this.$el)
        this.$el.click(this.action);
    },
});