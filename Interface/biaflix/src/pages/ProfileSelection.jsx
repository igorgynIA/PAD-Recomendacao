import brunoImg from '../imgs/bruno.png';
import andersonImg from '../imgs/anderson.png';
import federsonImg from '../imgs/federson.png';
import naoImg from '../imgs/nao.png';
import paulistaImg from '../imgs/paulista.png';
import './ProfileSelection.css'

import { Link } from 'react-router-dom';


function ProfileSelection() {
    // Array com os dados dos perfis para facilitar a manutenção
    const profiles = [
        { name: 'Bruno', img: brunoImg },
        { name: 'Anderson', img: andersonImg },
        { name: 'Federson', img: federsonImg },
        { name: 'NAO', img: naoImg },
        { name: 'Paulista', img: paulistaImg },
    ];

    return (
        <div className="d-flex justify-content-center align-items-center min-vh-100">
            <div className="container text-center">
                <h1 className="text-white display-4 mb-5">Quem está assistindo?</h1>
                <div className="row justify-content-center g-4 mb-5">
                    {profiles.map((profile, index) => (
                        <div key={index} className="col-4 col-sm-3 col-md-2">
                            {/* Troque <a> por <Link> */}
                            <Link to="/browse" className="profile-link">
                                <div className="profile-card">
                                    <img src={profile.img} className="img-fluid" alt={`Perfil ${profile.name}`} />
                                </div>
                                <span className="profile-name mt-2 d-block">{profile.name}</span>
                            </Link>
                        </div>
                    ))}
                </div>
                <button className="btn btn-outline-secondary btn-lg px-4">
                    GERENCIAR PERFIS
                </button>
            </div>
        </div>
    );
}

export default ProfileSelection;