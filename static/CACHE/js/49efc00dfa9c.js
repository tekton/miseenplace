var converter=new Showdown.converter();var DDoc=React.createClass({displayName:'DDoc',render:function(){return(React.createElement("div",{className:"defaultDoc"},this.props._id));}});var DDocList=React.createClass({displayName:'DDocList',render:function(){var documentNodes=this.props.data.map(function(d){console.log(d._id);return(React.createElement(DDoc,{_id:d}));});return(React.createElement("div",{className:"documentsList"},documentNodes));}});var D=React.createClass({displayName:'D',render:function(){return(React.createElement("div",null,this.props.author," ",this.props._id));}});var DDocContent=React.createClass({displayName:'DDocContent',loadDocsFromServer:function(){$.ajax({url:this.props.url,dataType:'json',success:function(data){console.log(data.docs);this.setState({data:data.docs});}.bind(this),error:function(xhr,status,err){console.error(this.props.url,status,err.toString());}.bind(this)});},componentDidMount:function(){this.loadDocsFromServer();console.log("componentDidMount");},getInitialState:function(){return{data:[]};},render:function(){return(React.createElement("div",{className:"ddocBox"},"This is random content",React.createElement(D,{author:"AUTHOR",_id:"_ID"}),React.createElement(DDocList,{data:this.state.data})));}});React.render(React.createElement(DDocContent,{url:"/api/company/1.0/docs",pollInterval:2000}),document.getElementById('docs'));