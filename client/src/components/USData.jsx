import axios from 'axios';
import { useEffect, useState } from 'react';
import Table from './Table';
import LinePlot from './LinePlot';

const Data = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        //data will be the string we send from our server
        const fetchData = () => {
            axios.get('http://localhost:8080/us').then((resp) => {
                const data = resp.data;
                setData(data)
            })
        }
        fetchData();
    }, []);

    return <>
        <h2>Records from ClinicalTrials.gov</h2>
        <Table data={data} />
    </>

    // return <LinePlot data={data} />
}

export default Data;