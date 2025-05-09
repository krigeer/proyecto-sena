function modifitInventari(){

    Swal.fire({
        title: "Elige una Opción",
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: "Añadir Tecnolgia",
        denyButtonText: `Añadir Material Didactico`
      }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
          location.href = "http://127.0.0.1:8000/bodega/newTecnologi/"
        } else if (result.isDenied) {
          location.href = "http://127.0.0.1:8000/bodega/newOtros/"
        }
      });
    // Swal.fire({
    //     title: "Elige una Opción",
    //     text: "You won't be able to revert this!",
    //     icon: "warning",
    //     showCancelButton: true,
    //     confirmButtonColor: "#3085d6",
    //     cancelButtonColor: "#d33",
    //     confirmButtonText: "Añadir Tecnolgia",
    //     cancelButtonText: "Añadir Material Didactico",
    //   }).then((result) => {
    //     if (result.isConfirmed) {
    //      location.href = "http://127.0.0.1:8000/newTecnologi"
    //     }else{
    //         location.href = "http://127.0.0.1:8000/newOtros"
    //     }
    //   });
}

