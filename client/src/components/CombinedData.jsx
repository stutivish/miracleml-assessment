import axios from 'axios';
import { useEffect, useState } from 'react';
import LinePlot from './LinePlot';
import Table from './Table';

const healthConditions = ['cancer', 'diabetes', 'smoking', 'psoriasis']

const Data = () => {
    const [dataMap, setDataMap] = useState({});

    useEffect(() => {
        const fetchData = async () => {
            try {
                const promises = healthConditions.map(async (condition) => {
                    const response = await axios.get(`http://localhost:8080/combined?type=conditions&term=${condition}`);
                    return { [condition]: response.data };
                });

                const results = await Promise.all(promises);
                const data = results.reduce((acc, curr) => {
                    const key = Object.keys(curr)[0];
                    acc[key] = curr[key];
                    return acc;
                }, {});

                setDataMap(data);
            } catch (error) {
                console.error('Error fetching data', error);
            }
        };

        fetchData();
    }, []);

    return (
        <div>
            {Object.entries(dataMap).map(([condition, results]) => {
                console.log('result:', results);
                return (
                    <div key={condition}>
                        <h2>{`${condition}: ${results.length}`}</h2>
                        <Table data={results} />
                    </div>
                )
            })}
        </div>
    );
};

export default Data;