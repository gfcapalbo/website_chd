$(document).ready(function () {

    $("#therp_trash").on('click', function (ev) {
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var $input = $link.parent().parent().find("input");
        $('input[name="'+$input.attr("name")+'"]').val(0);
        $input.change();
        return false;
    });

});