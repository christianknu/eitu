export default (url) => {
	const ajax = (method, url, data) => {
		return new Promise( (resolve, reject) => {
			const client = new XMLHttpRequest();

			client.open(method, url);
			client.setRequestHeader('Content-Type', 'application/json');
			client.send(data);

			client.onload = () => {
				if (client.status >= 200 && client.status < 300) resolve(client.response);  
				else reject(`${client.status}, ${client.statusText}`); 
			};
			client.onerror = () => reject(client.statusText);
		});
	};

	return {
		'get': (args) => ajax('GET', url, args),
		'post': (args) => ajax('POST', url, args),
		'put': (args) => ajax('PUT', url, args),
		'delete': (args) => ajax('DELETE', url, args)
	}
};
