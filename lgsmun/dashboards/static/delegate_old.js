async function routine_tasks(){

  if ($('#topic').html()=="No Topic Has Been Set"){

    getcurrenttopic();

  }
  if (($('#speaking_mode').html()=="Mod")&&($('#current_mod').html()=='No Moderated Caucus in Progress')){

    getcurrentmod();

  }
  else if($('#speaking_mode').html()!="Mod"){

    $('#current_mod').html('No Moderated Caucus in Progress');

  }

}
async function getattendance() {
  let x = await fetch("/dashboards/getcountrylist");
  let y = await x.text();
  $('#att').html(y);
}
async function getcurrentmod(){
  let x = await fetch("/dashboards/get_current_mod");
  let y = await x.text();
  $('#current_mod').html(y);
}
async function getspeakingmode(){
  let x = await fetch("/dashboards/get_speaking_mode");
  let y = await x.text();
  $('#speaking_mode').html(y);
}
async function getcurrenttopic(){
  let x = await fetch("/dashboards/get_current_topic");
  let y = await x.text();
  $('#topic').html(y);
}
setInterval(routine_tasks,1000)
setInterval(getattendance,1000);
setInterval(getspeakingmode,15000);
