import axios from 'axios';
import { useEffect, useState } from 'react';



const Data = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        //data will be the string we send from our server
        const fetchData = () => {
            axios.get('http://localhost:8080').then((resp) => {
                const data = resp.data;
                setData(data)
            })
        }
        fetchData();
    }, []);

    return <>{JSON.stringify(data)}</>
}

export default Data;