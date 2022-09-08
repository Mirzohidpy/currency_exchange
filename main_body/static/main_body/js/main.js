$(document).ready(function (){
    var csrf = $("input[name=csrfmiddlewaretoken]").val()
    $(".swap").click(function (){
        $.ajax({
            ulr:'',
            type:'post',
            data: {
                first:$(this).text(),
                second:$(this).text(),
                amount2:$(this).text(),

            },
            success: function (response) {
                $(".swap").text(response)
            }
        });
    });
});