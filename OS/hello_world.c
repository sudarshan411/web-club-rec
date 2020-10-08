#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

MODULE_LICENSE("GPL");   //to avoid the license warnings
MODULE_AUTHOR("Sudarshan");
MODULE_DESCRIPTION("first world");

static int world_init(void)		//init function
{
	printk(KERN_INFO "Hello, world!\n");
	return 0;
}

static void world_destroy(void)		//cleanup function
{
	printk(KERN_INFO "Bye, world!\n");
	return 0;
}

module_init(world_init);
module_exit(world_destroy);
