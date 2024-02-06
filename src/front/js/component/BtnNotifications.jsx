import React, { useContext } from "react";
import { Context } from "../store/appContext.js";
import { Link } from "react-router-dom";

export const BtnNotifications = () =>{
    const { store, actions } = useContext(Context);

    return(
    store.isInfluencer == true ? 
    <div>

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
                    <button type="button" className="btn btn-ligth" ><i class="fa-solid fa-check"></i></button>
                </li>
                )
            }))}
          </ul>
    </div>
    )
}