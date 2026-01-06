from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

@receiver(post_save, sender=User)
def assign_user_group(sender, instance, created, **kwargs):
    """
    Assign user to a group based on their role.
    Removes user from other role-based groups.
    """
    role_map = {
        User.Roles.READER: 'Reader',
        User.Roles.JOURNALIST: 'Journalist',
        User.Roles.EDITOR: 'Editor'
    }
    
    target_group_name = role_map.get(instance.role)
    if target_group_name:
        target_group = Group.objects.filter(name=target_group_name).first()
        if target_group:
            # Add to the new group
            instance.groups.add(target_group)
            
            # Remove from other role groups
            for r_key, g_name in role_map.items():
                if g_name != target_group_name:
                    g = Group.objects.filter(name=g_name).first()
                    if g:
                        instance.groups.remove(g)

    # Cleanup Reader fields if not a Reader
    if instance.role != User.Roles.READER:
        instance.subscriptions_to_publishers.clear()
        instance.subscriptions_to_journalists.clear()
