const Table = ({ data }) => {
    return (
        <table style={{ border: '1px solid black', borderCollapse: 'collapse' }}>
            <tr>
                <th style={{ border: '1px solid black', textAlign: 'left', padding: '8px' }}>Study Id</th>
                <th style={{ border: '1px solid black', textAlign: 'left', padding: '8px' }}>Study Title</th>
                <th style={{ border: '1px solid black', textAlign: 'left', padding: '8px' }}>Conditions</th>
                <th style={{ border: '1px solid black', textAlign: 'left', padding: '8px' }}>Sponsor</th>
            </tr>
            {data.map((val) => {
                return (
                    <tr key={val.study_id}>
                        <td style={{ border: '1px solid black', padding: '8px' }}>{val.study_id}</td>
                        <td style={{ border: '1px solid black', padding: '8px' }}>{val.study_title}</td>
                        <td style={{ border: '1px solid black', padding: '8px' }}>{val.conditions}</td>
                        <td style={{ border: '1px solid black', padding: '8px' }}>{val.sponsor}</td>
                    </tr>
                )
            })}
        </table>
    )
}

export default Table;