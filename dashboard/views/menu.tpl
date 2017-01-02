<ul class="sidebar-menu">
    <li class="header">{{title}}</li>
    % for label, entry in entries:
        <li class="{{'active' if label==active_page else ''}}">
            <a href="{{url(entry.name)}}">
                <i class="{{entry.icon}}"></i><span>{{entry.title}}</span>
            </a>
        </li>
    % end
</ul>