import { createDriver } from 'use-neo4j';

const DEFAULT_DB_SETTINGS = {
  neo4jHost: 'localhost',
  neo4jPort: '7687',
  neo4jUsername: '',
  neo4jPassword: '',
};

const ConnectDatabase = ({ driver, setDriver, nextStep }) => {
  const [dbSettings, setDbSettings] = useState(DEFAULT_DB_SETTINGS);
  const onConnectDb = () => {
    const connectionDriver = createDriver(
      'bolt',
      dbSettings.neo4jHost,
      dbSettings.neo4jPort,
      dbSettings.neo4jUsername,
      dbSettings.neo4jPassword,
    );

    connectionDriver
      .verifyConnectivity()
      .then(() => {
        setDriver(connectionDriver);
      })
      .catch((err) => {
        // handle wrong connection settings
      })
  };

  return (
    <form onSubmit={onConnectDb}>
     // Form component for host, username, port, password
    </form>
  )
}
