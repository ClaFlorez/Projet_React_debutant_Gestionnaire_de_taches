const tasks = [
  { id: 1, title: "Lire le rapport", done: true },
  { id: 2, title: "Vérifier les alertes", done: false },
];

console.log(tasks[0].title);

const remainingTasks = tasks.filter((task) => !task.done);
console.log(remainingTasks.length);