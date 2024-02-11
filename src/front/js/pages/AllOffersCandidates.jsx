import React, { useContext } from "react";
import { Context } from "../store/appContext.js";
import { Link } from "react-router-dom";

export const AllOffersCandidates = () =>{
    const { store, actions } = useContext(Context);

    return(
        <div>
            <h1 className="text-center mt-5 title-style">Listado de candidaturas</h1>
            <div className="d-flex justify-content-center">
            <h3 className="text-center mt-1 title-style col-8" style={{fontSize: "30px"}}>Selecciona una oferta para ver los candidatos de la misma</h3>
            </div>
            <div className="container-fluid mt-5">
              {!store.candidatesOffersAll ?
                <div className="alert alert-warning m-2" role="alert">
                    No tienes candidaturas en tus ofertas actuales.
                </div>
              :(store.offersCompany.map((item, id) =>{
                return(
                    <div className="d-flex justify-content-center">
                    <div className="p-4 col-8 m-2 mb-3 border rounded text-start d-flex justify-content-between " style={{background: "#FFC66B"}}>
                            <div>
                                <h4 className="m-1 ps-3">Título: {item.title}</h4>
                                <p className="m-1 ps-3">Descripción: {item.post}</p>
                                <p className="m-1 ps-3">Estado de la oferta: {item.status == "opened" ? "Abierta" : "Cerrada/Cancelada"}</p>
                            </div>
                            <div>
                                <Link to={`/company/my-offers/${item.id}/influencers`} className="bg-secondary text-secondary">
                                    <p className="text-end m-1 me-3 text-secondary me-1 ms-2"><i className="fa-regular fa-eye fa-lg text-secondary me-2"></i>Ver candidatos de esta oferta</p>
                                </Link>
                            </div>
                    </div>
                    </div>
                )
              })
              )}  

            </div>
        </div>
    )
}