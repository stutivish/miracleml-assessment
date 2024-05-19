import axios from 'axios';
import { useEffect, useState } from 'react';
import Table from './Table';

const Data = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
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
}

export default Data;