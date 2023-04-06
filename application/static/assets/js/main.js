// var socket = new WebSocket("ws://localhost:8000/ws/teaching/");
// socket.onmessage = function(event){
//   var data = JSON.parse(event.data);
//   console.log(data)
// }
const fileInput = document.getElementById('samples')
const features=document.getElementById("features")
const target= document.getElementById("target")
const teach= document.getElementById("teach")
var file=""
var header=""
var skill=""
//For security propurse
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

var specification={
}


function getCurrent(){
  queryString=window.location.search
  queryString =new URLSearchParams(queryString)
  skill= queryString.get('type')

}

getCurrent()



teach.addEventListener('click',teachskill)
settings= document.getElementById("settings")

const readFile = () =>{
    const reader = new FileReader()
    reader.onloadstart =() =>{
      target.innerHTML =''
      features.innerHTML = ''
      file=""
      header=""
      target.innerHTML=''
    }
    reader.onload = () =>{
      // console.log(reader.result)
      savefile(reader.result);
      extractheader(file);
      settings.style.display="initial"
      showfeatures();
    }

    reader.onloadend= () =>{
      
    }
    

    reader.readAsBinaryString(fileInput.files[0])

    

    
}

fileInput.addEventListener('change', readFile)


function savefile(text){
  file=file+text;

}

function teachskill(){
  getCurrent()
  if (specification['features'] && specification['file'] && specification['target']  ){
    specification['skill']=skill
    fetch("/teaching",{
      credentials: 'same-origin',
      method :"POST",
      headers:{
        'Cotent-Type':"application/json",
        'X-CSRFToken': csrftoken
      },
      body : JSON.stringify({payload : specification })
    }).then(response => response.json())
    .then( (data) =>{
      document.getElementById('result').style.display="none"
      document.getElementById('label1').innerHTML=''
      document.getElementById('label2').innerHTML=''
      document.getElementById('label3').innerHTML=''
      if (data.accuracy){
        document.getElementById('result').style.display="initial"
        document.getElementById("progress1").value=data.accuracy*100
        document.getElementById('label1').appendChild(document.createTextNode('Precision'))
        document.getElementById("progress2").value=data.precision*100
        document.getElementById('label2').appendChild(document.createTextNode('Accuracy'))
        document.getElementById("progress3").value=data.recall*100
        document.getElementById('label3').appendChild(document.createTextNode('Recall'))
      }
      console.log(data);
      if(data.pinball_score){
        document.getElementById('result').style.display="initial"
        document.getElementById("progress1").value=data.explained_variance_score*100
        document.getElementById('label1').appendChild(document.createTextNode('Explained variance'))
        document.getElementById("progress2").value=data.pinball_score*100
        document.getElementById('label2').appendChild(document.createTextNode('Pinball'))
        document.getElementById("progress3").value=data.d2_tweedie_score*100
        document.getElementById('label3').appendChild(document.createTextNode('D2 tweedie'))
      }
      
      
    })
    .catch( e => {console.error(e)}
    )

  }else{
    console.log("Data unset");
    // window.confirm("Welcome back");
  }
  
}

function extractheader(file){
  header=file.split("\r\n")[0]
  header=header.split(",")
  console.log(header)
}


function showfeatures(){
  

  
    header.forEach(element => {
      // create features nodes
      p = document.createElement("p")
      text = document.createTextNode(element)
      p.appendChild(text)
  
      // create target 
      
      option = document.createElement("option")
      option.value=element
      option.text=element
      target.add(option)
      features.appendChild(p)
      
    });
  
  document.getElementById("target").addEventListener('change',targetselect)
}

function setFeatures(target){
  new_list = header.slice()
  delete new_list[target]
  features.innerHTML = ''
  refreshFeatures(new_list)
  specification['features']=new_list
  console.log(specification)
  specification['file']=file
}

function targetselect(){
  refreshFeatures(header)
  let x=document.getElementById("target").selectedIndex;
  specification['target']=document.getElementsByTagName("option")[x].value
  setFeatures(x)
}


function refreshFeatures(new_feature){
 
    new_feature.forEach(element => {
    p = document.createElement("p")
    text = document.createTextNode(element)
    p.appendChild(text)
    features.appendChild(p)
  });
  
}