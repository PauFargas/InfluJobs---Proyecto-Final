import React, { useContext } from "react";
import { Context } from "../store/appContext.js";
import { Link } from "react-router-dom";

export const BtnNotifications = () =>{
    const { store, actions } = useContext(Context);

    return(
    store.isInfluencer == true ? 
    <div className="dropdown dropstart me-3 d-sm-none d-md-block">
        <button type="button" className="btn btn-warning m-2 color-button dropdown-toggle position-relative" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false"><i className="fa-regular fa-bell fa-lg pe-2"></i>Candidaturas
        <span className="position-absolute top-0 start-100 translate-middle p-2 bg-danger rounded-circle">
            <span className="visually-hidden">New alerts</span>
        </span>
        </button>
        <ul className="dropdown-menu" aria-labelledby="dropdownMenuButton1">
            {!store.registerCandidates ? (
                <li><a className="dropdown-item" href="#">No tienes notificaciones.</a></li>
            ) : (
            store.registerCandidates.map((item, id)=>{
                if (`${item.status_candidate}` == "accepted" || `${item.status_candidate}` == "refused"){
                    return ( 
                    <li key={item.id} className="d-flex">
                        <Link to={`/update-offer/${item.id}`} className="dropdown-item" >{item.offer.title}</Link>
                        <p className="dropdown-item border rounded">{item.status_candidate == "accepted" ? "Aceptado" : "Rechazado"}</p>
                        <button type="button" className="btn btn-ligth"><i class="fa-solid fa-check"></i></button>
                    </li>
                )}
            }))}
            <li className="d-flex text-center bg-secondary "><Link className="dropdown-item text-light" to="/offer-candidates">Ver todas</Link></li> 
          </ul>
    </div>
    :
    <div className="dropdown dropstart me-3 d-sm-none d-md-block">
        <button type="button" className="btn btn-warning m-2 color-button dropdown-toggle position-relative" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false"><i className="fa-regular fa-bell fa-lg pe-2"></i>Candidatos
        <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
            {!store.candidatesOffersAll ? "0" : store.candidatesOffersAll.length}
            <span className="visually-hidden">New alerts</span>
        </span>
        </button>
        <ul className="dropdown-menu" aria-labelledby="dropdownMenuButton1">
            {!store.candidatesOffersAll ? (
                <li><a className="dropdown-item" href="#">No tienes candidatos en tus ofertas.</a></li>
            ) : (
            store.candidatesOffersAll.map((item, id)=>{
             return ( 
                <li key={item.id} className="d-flex">
                    <Link to={`/update-offer/${item.id}`} className="dropdown-item" >{item.influencer.first_name} {item.influencer.last_name}</Link>
                    <p>Seguidores: {item.followers}</p>
                    <button type="button" className="btn btn-ligth"><i class="fa-solid fa-check"></i></button>
                </li>
                )
            }))}
            <li className="d-flex text-center bg-secondary "><Link className="dropdown-item text-light" to="/company/my-offers/all-candidates">Ver todos</Link></li> 
          </ul>
    </div>
    )
}