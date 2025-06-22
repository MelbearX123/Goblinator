export default function NavBar(){
  return(
    <nav className="sticky top-0 bg-black shadow px-6 py-8 flex justify-between items-center">
      <a className="text-3xl text-white font-bold text-shadow-xs">
        Goblinator
      </a>
      <ul className="flex gap-4 sm:gap-6 text-sm sm:text-base text-gray-300 font-medium">
        <li className="text-white text-0.5xl">Made by Silverhand</li>
      </ul>
    </nav>
  );
}