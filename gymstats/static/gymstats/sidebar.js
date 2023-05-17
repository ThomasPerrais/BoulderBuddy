const sidebar = document.querySelector(".w3-sidebar");

const sidebarMenus = {
    "fa-home": "/gymstats/home",
    "fa-user-ninja": "/gymstats/profil",
    "fa-chart-pie": "/gymstats/statistics",
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