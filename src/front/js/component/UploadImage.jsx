import React, { useContext, useState } from "react";
import { Context } from "../store/appContext.js";

export const UploadImage = () => {
  const { store, actions } = useContext(Context);
  const [files, setFiles] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);


  const uploadFile = (e) => {
    e.preventDefault();
    if (files) {
      actions.uploadFile(files[0]);
    }
  };

  const handleFileChange = (e) => {
    setFiles(e.target.files);
    if (e.target.files && e.target.files[0]) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreviewImage(e.target.result);
      };
      reader.readAsDataURL(e.target.files[0]);
    }
  };
  const handleReset = () => {
    setFiles(null);
    setPreviewImage(null);
    window.location.reload(); 
  };

  return (
    <div className="container">
      <h3><small>Subir imagen</small></h3>
      <div className="mb-3">
        <input type="file" className="form-control" onChange={handleFileChange} />
      </div>
      <button className="btn btn-primary me-3" onClick={uploadFile}>
        Subir
      </button>
      <button onClick={handleReset} className="btn btn-primary mx-3" type="reset">Cancelar</button>
      {!store.imageProfile ?
      <div></div>
      :
      <div className="alert alert-success m-5" role="alert">
          Imagen subida satisfactoriamente!
      </div>
      }
      <div className="mt-3">
        {previewImage && (
          <div>
            <h4>Imagen Seleccionada:</h4>
            <img className="img-thumbnail" style={{objectFit: "cover", aspectRatio: "1/1", maxHeight: "30%", maxWidth: "30%"}} src={previewImage} alt="Imagen Seleccionada" />
          </div>
        )}
      </div>
    </div>
  );
};