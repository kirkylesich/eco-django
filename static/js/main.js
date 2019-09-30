var res = $(".dropdown-menu");
$(".knop").on("click", funk);


function funk(){
  if(res.css("display") == "none"){
    res.fadeIn(100);
  }
  else{
    res.fadeOut(100);
  }
}