import 'bootstrap/dist/css/bootstrap.min.css';

const LeaderCard = ({ entity }) => {
    return (
        <div className="card mb-3" style={{ maxWidth: '540px' }}>
            <div className="row g-0">
                <div className="col-md-4">
                    <img src="https://via.placeholder.com/150" className="img-fluid rounded-start position-relative top-50 start-50 translate-middle" alt="Entity" />
                </div>
                <div className="col-md-8">
                    <div className="card-body">
                        <h5 className="card-title">{entity.name}</h5>
                        <div className="progress" style={{ height: '25px' }}>
                            <div
                                className="progress-bar"
                                role="progressbar"
                                style={{ width: `${entity.foodLevel}%` }}
                                aria-valuenow={entity.foodLevel}
                                aria-valuemin="0"
                                aria-valuemax="100"
                            >
                                {entity.foodLevel}%
                            </div>
                        </div>
                        <p className="card-text mt-2"><small className="text-muted">LeaderBoard Entry</small></p>
                    </div>
                </div>
            </div>
        </div>
    );
};

const LeaderBoard = ({ entities }) => {
    return (
            <div className="container">
                {entities.map((entity, index) => (
                    <div className="row" key={index}>
                        <LeaderCard entity={entity} />
                    </div>
                ))}
            </div>
        );
};

export default LeaderBoard;
