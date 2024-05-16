#include<cstdio>
#include<algorithm>
#include<cstring>
#define maxn 1001000
using namespace std;
int n,head[maxn],k,a[maxn],Min1[maxn],Min2[maxn],Size[maxn],ans[maxn];
struct node{
    int to,next;
}edge[maxn<<1];
void add(int u,int v){
    edge[++k].next=head[u];
    edge[k].to=v;
    head[u]=k;
}
void dfs(int u,int Fa){
    Size[u]=1;
    Min1[u]=a[u];
    for(int i=head[u];i;i=edge[i].next){
        int v=edge[i].to;
        if(v==Fa) continue;
        dfs(v,u);
        if(Min1[u]>Min1[v]) Min2[u]=Min1[u],Min1[u]=Min1[v];
        else Min2[u]=min(Min2[u],Min1[v]);
        Size[u]+=Size[v];
    }
}
void solve(int u,int Fa){
    int Ans=0;
    for(int i=head[u];i;i=edge[i].next){
        int v=edge[i].to;
        if(v==Fa) continue;
        solve(v,u);
        if(Min1[u]==min(Min1[v],a[v])) Ans=Size[v];
        if(a[u]==0) ans[0]=max(ans[0],Size[v]);
    }
    if(a[u]==0){
        ans[0]=max(ans[0],n-Size[u]);
        return ;
    }
    if(Min2[u]<a[u] && Min1[u]<a[u]) return ;
    int temp=maxn;
    if(u!=1) temp=min(Min1[Fa],a[Fa]);
    if(temp==Min1[u] || temp==a[u]) temp=min(Min2[Fa],a[Fa]);
    if(temp<a[u] && Min1[u]<a[u]) return ;
    if(Min1[u]<a[u]) ans[a[u]]=Ans;
    else ans[a[u]]=n-Size[u];
}
int main(){
    scanf("%d",&n);
    for(int i=1;i<=n;i++) scanf("%d",&a[i]);
    for(int i=2,v;i<=n;i++) scanf("%d",&v),add(i,v),add(v,i);
    memset(Min1,127,sizeof Min1);
    memset(Min2,127,sizeof Min2);
    dfs(1,1);
    solve(1,1);
    ans[n]=n;
    for(int i=0;i<=n;i++) printf("%d ",ans[i]);
    return 0;
}