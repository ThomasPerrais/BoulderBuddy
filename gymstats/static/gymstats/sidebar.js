const sidebar = document.querySelector(".w3-sidebar");

const sidebarMenus = {
    "fa-calendar": "/gymstats/home",
    "fa-user-ninja": "/gymstats/profil",
    "fa-chart-pie": "/gymstats/statistics",
    "fa-mountain-city": "/gymstats/gyms",
    "fa-magnifying-glass": "/gymstats/problems/searchbar"
};

function LoadSidebar() {
    divTag = "";
    for (var elt in sidebarMenus) {
        divTag += `<a href="${sidebarMenus[elt]}" class="w3-bar-item w3-button"><i class="fa ${elt}"></i></a>`
    }
    sidebar.innerHTML += divTag;
}

LoadSidebar();