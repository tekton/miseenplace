/** @jsx React.DOM */
// default_docs.js

var converter = new Showdown.converter();

var DDoc = React.createClass({
    render: function() {
        var hh="/default/"+this.props.d._id+"/view";
        return (
            <div className="defaultDoc">
                <a href={hh}>{this.props.d._id}</a>
            </div>
        );
    }
});

var DDocList = React.createClass({
    render: function() {
        var documentNodes = this.props.data.map(function (d) {
            console.log(d._id);
            return (
                <DDoc d={d} key={d._id}/>
            );
        });
        // return (
        //     <div className="documentsList">
        //         {documentNodes}
        //     </div>
        // );
        return (
            <div className="documentsList">
                {documentNodes}
            </div>
        );
    }
});

var D = React.createClass({
    render: function() {
        return (<div>{this.props.author} {this.props._id}</div>);
    }
});

var DDocContent = React.createClass({
    loadDocsFromServer: function() {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            success: function(data) {
                console.log(data.docs);
                this.setState({data: data.docs});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(this.props.url, status, err.toString());
            }.bind(this)
        });
    },
    componentDidMount: function() {
        this.loadDocsFromServer();
        console.log("componentDidMount");
        setInterval(this.loadDocsFromServer, this.props.pollInterval);
    },
    getInitialState: function() {
        return {data: []};
    },
    render: function() {
        return (
            <div className="ddocBox">
                This is random content
                <D author="AUTHOR" _id="_ID" />
                <DDocList data={this.state.data} url={this.props.url} />
            </div>
        );
    }
});

// React.render(
//   <DDocContent url="/api/company/1.0/docs" pollInterval={2000} />,
//   document.getElementById('docs_xyz')
// );