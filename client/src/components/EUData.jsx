import axios from 'axios';
import { useEffect, useState } from 'react';
import LinePlot from './LinePlot';

const Data = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        const fetchData = () => {
            axios.get('http://localhost:8080/eu').then((resp) => {
                const data = resp.data;
                setData(data)
            })
        }
        fetchData();
    }, []);

    return <div style={{ textAlign: 'center' }}><LinePlot data={data} /></div>
}

export default Data;