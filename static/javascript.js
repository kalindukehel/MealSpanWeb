function generateDate() {
  var d = new Date();
  var year = d.getFullYear();
  var month = d.getMonth();
  if(month>=0 && month <=3){
  	document.getElementById("date").value = year+"-04-21";
  }else if(month>=8 && month<=11){
  	document.getElementById("date").value = year+"-12-14";
  }else if(month>=4 && month<=7){
  	document.getElementById("date").value = year+"-08-15";
  }
}
