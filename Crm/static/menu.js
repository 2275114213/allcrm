$('.item .title').click(function () {
    // $(this).removeClass('show')
    // $(this).next().removeClass('show')
    // $(this).parent().siblings().children(".body").removeClass('show')
    $(this).next().toggleClass('hide');
    $(this).parent().siblings().children(".body").addClass("hide")
});


// $('.body a').attr("href").each(j,function () {
//   if(j===request.path){
//      $(this).removeClass("hide")
//   }
// })