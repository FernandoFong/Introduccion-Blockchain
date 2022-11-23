// SPDX-License-Identifier: MIT

pragma solidity >= 0.6.0 < 0.9.0;

    /*
    * Un diccionario emula el comportamiento de un arreglo, pero con la condicion de que
    * los indices no necesariamente sean numeros.
    * d = {}
    * d["Fernando"] = "Hola"
    * A estos indices, se les conocen como llaves y la condicion es que la llave siempre
    * debe de ser unica.
    * Diccionario<Object, int>
    */

contract SimpleStorage { //Simulando el almacen de un banco.

    struct Account {
        uint256 favNum;
        string name;
    }


    Account [] public accounts;
    //Mapping (Diccionario)
    mapping(string => uint256) public diccionario;
    uint256 num;

    function addAccount(uint256 _number, string memory _name) public {
        accounts.push(Account(_number, _name));
        diccionario[_name] = _number;
    }

    function getNumber(string memory _name) public view returns(uint256) {
        return diccionario[_name];
    }

    function store(uint256 _num) public {
        num = _num;
    }

    function retrieve() public view returns (uint256) {
        return num;
    }

}